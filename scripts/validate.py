#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPOSITORY_ROOT / "proposals" / "schema.json"
PROPOSAL_FILE_PATTERN = re.compile(r"^NJ-P-[0-9]{4}\.json$")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

REQUIRED_PATHS = (
	"README.md",
	"CHARTER.md",
	"GOVERNANCE.md",
	"CONTRIBUTING.md",
	"AGENTS.md",
	"OPEN_QUESTIONS.md",
	"VERSION",
	"LICENSE",
	"law/README.md",
	"proposals/README.md",
	"proposals/schema.json",
	"cases/README.md",
	"evaluations/README.md",
	"research/README.md",
	".github/PULL_REQUEST_TEMPLATE.md",
	".github/ISSUE_TEMPLATE/legal-problem.md",
	".github/ISSUE_TEMPLATE/proposal-request.md",
	".github/workflows/validate.yml",
)


def loadJson(path, errors):
	try:
		with path.open("r", encoding="utf-8") as file:
			return json.load(file)
	except FileNotFoundError:
		errors.append(f"{path}: file does not exist")
	except json.JSONDecodeError as error:
		errors.append(f"{path}:{error.lineno}:{error.colno}: invalid JSON: {error.msg}")

	return None


def isSchemaType(value, expectedType):
	if expectedType == "object":
		return isinstance(value, dict)

	if expectedType == "array":
		return isinstance(value, list)

	if expectedType == "string":
		return isinstance(value, str)

	if expectedType == "integer":
		return isinstance(value, int) and isinstance(value, bool) == False

	if expectedType == "number":
		return isinstance(value, (int, float)) and isinstance(value, bool) == False

	if expectedType == "boolean":
		return isinstance(value, bool)

	if expectedType == "null":
		return value is None

	return False


def getJsonKey(value):
	return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validateSchemaValue(value, schema, location, errors):
	if "const" in schema and value != schema["const"]:
		errors.append(f"{location}: must equal {schema['const']!r}")

	if "enum" in schema and value not in schema["enum"]:
		errors.append(f"{location}: value {value!r} is not in the allowed set")

	expectedType = schema.get("type")
	if expectedType is not None and isSchemaType(value, expectedType) == False:
		errors.append(f"{location}: expected {expectedType}")
		return

	if isinstance(value, str):
		minimumLength = schema.get("minLength")
		if minimumLength is not None and len(value) < minimumLength:
			errors.append(f"{location}: string is shorter than {minimumLength}")

		pattern = schema.get("pattern")
		if pattern is not None and re.search(pattern, value) is None:
			errors.append(f"{location}: value {value!r} does not match {pattern!r}")

	if isinstance(value, list):
		minimumItems = schema.get("minItems")
		if minimumItems is not None and len(value) < minimumItems:
			errors.append(f"{location}: array has fewer than {minimumItems} items")

		if schema.get("uniqueItems") == True:
			seenItems = set()
			for index, item in enumerate(value):
				itemKey = getJsonKey(item)
				if itemKey in seenItems:
					errors.append(f"{location}[{index}]: duplicate array item")
				seenItems.add(itemKey)

		itemSchema = schema.get("items")
		if itemSchema is not None:
			for index, item in enumerate(value):
				validateSchemaValue(item, itemSchema, f"{location}[{index}]", errors)

	if isinstance(value, dict):
		properties = schema.get("properties", {})
		for requiredKey in schema.get("required", []):
			if requiredKey not in value:
				errors.append(f"{location}: missing required property {requiredKey!r}")

		if schema.get("additionalProperties") == False:
			for key in value:
				if key not in properties:
					errors.append(f"{location}: unexpected property {key!r}")

		for key, propertySchema in properties.items():
			if key in value:
				validateSchemaValue(value[key], propertySchema, f"{location}.{key}", errors)


def validateSchemaDocument(schema, errors):
	if isinstance(schema, dict) == False:
		errors.append(f"{SCHEMA_PATH}: schema root must be an object")
		return

	if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
		errors.append(f"{SCHEMA_PATH}: unsupported JSON Schema declaration")

	if schema.get("type") != "object":
		errors.append(f"{SCHEMA_PATH}: proposal root type must be object")

	properties = schema.get("properties")
	if isinstance(properties, dict) == False:
		errors.append(f"{SCHEMA_PATH}: properties must be an object")
		return

	schemaVersion = properties.get("schemaVersion", {}).get("const")
	if schemaVersion != "0.1":
		errors.append(f"{SCHEMA_PATH}: supported schemaVersion must be '0.1'")


def getProposalFiles(repositoryRoot):
	proposalDirectory = repositoryRoot / "proposals"
	return sorted(proposalDirectory.glob("NJ-P-*.json"))


def resolveRepositoryPath(reference, repositoryRoot, location, errors):
	if reference.startswith("/"):
		errors.append(f"{location}: path must be repository-relative: {reference!r}")
		return None

	repositoryPath = repositoryRoot.resolve()
	referencedPath = (repositoryRoot / reference).resolve()

	if referencedPath != repositoryPath and repositoryPath not in referencedPath.parents:
		errors.append(f"{location}: path leaves the repository: {reference!r}")
		return None

	if referencedPath.is_file() == False:
		errors.append(f"{location}: referenced file does not exist: {reference!r}")
		return None

	return referencedPath


def validateAuthorship(proposal, location, errors):
	authorship = proposal.get("authorship")
	if isinstance(authorship, dict) == False:
		return

	mode = authorship.get("mode")
	aiSystems = authorship.get("aiSystems")
	if isinstance(aiSystems, list) == False:
		return

	if mode == "human_authored" and len(aiSystems) != 0:
		errors.append(f"{location}.authorship.aiSystems: human_authored proposals must use an empty list")

	if mode != "human_authored" and mode is not None and len(aiSystems) == 0:
		errors.append(f"{location}.authorship.aiSystems: this authorship mode requires at least one AI system")


def validateProposalReferences(proposal, proposalIds, repositoryRoot, location, errors):
	for index, reference in enumerate(proposal.get("affectedProvisions", [])):
		if isinstance(reference, str):
			resolveRepositoryPath(reference, repositoryRoot, f"{location}.affectedProvisions[{index}]", errors)

	for index, reference in enumerate(proposal.get("testCases", [])):
		if isinstance(reference, str):
			resolveRepositoryPath(reference, repositoryRoot, f"{location}.testCases[{index}]", errors)

	for index, dependency in enumerate(proposal.get("dependencies", [])):
		if isinstance(dependency, dict) == False:
			continue

		kind = dependency.get("kind")
		reference = dependency.get("reference")
		dependencyLocation = f"{location}.dependencies[{index}].reference"

		if kind == "provision" and isinstance(reference, str):
			resolveRepositoryPath(reference, repositoryRoot, dependencyLocation, errors)

		if kind == "proposal" and isinstance(reference, str) and reference not in proposalIds:
			errors.append(f"{dependencyLocation}: proposal does not exist: {reference!r}")


def validateProposal(path, schema, proposalIds, repositoryRoot, isRepositoryRecord):
	errors = []
	proposal = loadJson(path, errors)
	if proposal is None:
		return errors, None

	validateSchemaValue(proposal, schema, str(path), errors)

	if isinstance(proposal, dict):
		proposalId = proposal.get("id")
		if isRepositoryRecord == True:
			expectedFilename = f"{proposalId}.json"
			if path.name != expectedFilename:
				errors.append(f"{path}: filename must be {expectedFilename!r}")

		validateAuthorship(proposal, str(path), errors)
		validateProposalReferences(proposal, proposalIds, repositoryRoot, str(path), errors)

	return errors, proposal


def validateRequiredPaths(repositoryRoot, errors):
	for relativePath in REQUIRED_PATHS:
		path = repositoryRoot / relativePath
		if path.is_file() == False:
			errors.append(f"{path}: required repository file is missing")


def validateVersion(repositoryRoot, errors):
	versionPath = repositoryRoot / "VERSION"
	if versionPath.is_file() == False:
		return

	version = versionPath.read_text(encoding="utf-8").strip()
	if version != "0.1":
		errors.append(f"{versionPath}: expected version '0.1', found {version!r}")


def getMarkdownFiles(repositoryRoot):
	return sorted(path for path in repositoryRoot.rglob("*.md") if ".git" not in path.parts)


def validateMarkdownLinks(repositoryRoot, errors):
	checkedLinks = 0

	for markdownPath in getMarkdownFiles(repositoryRoot):
		content = markdownPath.read_text(encoding="utf-8")
		for match in MARKDOWN_LINK_PATTERN.finditer(content):
			target = match.group(1).strip()
			if target.startswith("<") and target.endswith(">"):
				target = target[1:-1]

			if target.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
				continue

			pathPart = unquote(target.split("#", 1)[0])
			if pathPart == "":
				continue

			checkedLinks += 1
			if pathPart.startswith("/"):
				linkedPath = repositoryRoot / pathPart.lstrip("/")
			else:
				linkedPath = markdownPath.parent / pathPart

			if linkedPath.exists() == False:
				lineNumber = content.count("\n", 0, match.start()) + 1
				errors.append(f"{markdownPath}:{lineNumber}: broken internal link: {target!r}")

	return checkedLinks


def validateRepository(repositoryRoot=REPOSITORY_ROOT):
	errors = []
	validateRequiredPaths(repositoryRoot, errors)
	validateVersion(repositoryRoot, errors)

	schema = loadJson(repositoryRoot / "proposals" / "schema.json", errors)
	if schema is None:
		return errors, 0, 0

	validateSchemaDocument(schema, errors)
	proposalFiles = getProposalFiles(repositoryRoot)
	proposalIds = set()
	loadedProposals = []

	for path in proposalFiles:
		proposal = loadJson(path, errors)
		if isinstance(proposal, dict):
			proposalId = proposal.get("id")
			if proposalId in proposalIds:
				errors.append(f"{path}: duplicate proposal id {proposalId!r}")
			if isinstance(proposalId, str):
				proposalIds.add(proposalId)
			loadedProposals.append((path, proposal))

	for path, proposal in loadedProposals:
		proposalErrors = []
		validateSchemaValue(proposal, schema, str(path), proposalErrors)

		proposalId = proposal.get("id")
		expectedFilename = f"{proposalId}.json"
		if path.name != expectedFilename:
			proposalErrors.append(f"{path}: filename must be {expectedFilename!r}")

		validateAuthorship(proposal, str(path), proposalErrors)
		validateProposalReferences(proposal, proposalIds, repositoryRoot, str(path), proposalErrors)
		errors.extend(proposalErrors)

	checkedLinks = validateMarkdownLinks(repositoryRoot, errors)
	return errors, len(proposalFiles), checkedLinks


def printErrors(errors):
	for error in errors:
		print(f"ERROR: {error}", file=sys.stderr)


def main():
	parser = argparse.ArgumentParser(description="Validate the New Jurisdiction repository and proposal records.")
	parser.add_argument("--proposal", type=Path, help="Validate one proposal file against the repository schema.")
	arguments = parser.parse_args()

	if arguments.proposal is not None:
		errors = []
		schema = loadJson(SCHEMA_PATH, errors)
		if schema is None:
			printErrors(errors)
			return 1

		validateSchemaDocument(schema, errors)
		proposalIds = set()
		for path in getProposalFiles(REPOSITORY_ROOT):
			proposal = loadJson(path, errors)
			if isinstance(proposal, dict) and isinstance(proposal.get("id"), str):
				proposalIds.add(proposal["id"])

		proposalErrors, proposal = validateProposal(
			arguments.proposal.resolve(),
			schema,
			proposalIds,
			REPOSITORY_ROOT,
			False,
		)
		errors.extend(proposalErrors)

		if len(errors) != 0:
			printErrors(errors)
			return 1

		print(f"Valid proposal: {arguments.proposal}")
		return 0

	errors, proposalCount, linkCount = validateRepository(REPOSITORY_ROOT)
	if len(errors) != 0:
		printErrors(errors)
		return 1

	print(f"Validated repository: {proposalCount} proposal records, {linkCount} internal Markdown links")
	return 0


if __name__ == "__main__":
	sys.exit(main())
