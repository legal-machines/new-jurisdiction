import copy
import importlib.util
import json
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate.py"

validatorSpec = importlib.util.spec_from_file_location("new_jurisdiction_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(validatorSpec)
validatorSpec.loader.exec_module(validator)


class ValidateRepositoryTest(unittest.TestCase):
	def loadSchema(self):
		with (REPOSITORY_ROOT / "proposals" / "schema.json").open("r", encoding="utf-8") as file:
			return json.load(file)

	def loadTemplate(self):
		with (REPOSITORY_ROOT / "proposals" / "TEMPLATE.json").open("r", encoding="utf-8") as file:
			return json.load(file)

	def testRepositoryIsValid(self):
		errors, proposalCount, linkCount = validator.validateRepository(REPOSITORY_ROOT)

		self.assertEqual(errors, [])
		self.assertEqual(proposalCount, 0)
		self.assertGreater(linkCount, 0)

	def testInvalidFixtureFails(self):
		schema = self.loadSchema()
		fixturePath = REPOSITORY_ROOT / "tests" / "fixtures" / "invalid-proposal.json"
		errors, proposal = validator.validateProposal(
			fixturePath,
			schema,
			set(),
			REPOSITORY_ROOT,
			False,
		)

		self.assertIsNotNone(proposal)
		self.assertGreater(len(errors), 0)

	def testTemplateIsValid(self):
		schema = self.loadSchema()
		templatePath = REPOSITORY_ROOT / "proposals" / "TEMPLATE.json"
		errors, proposal = validator.validateProposal(
			templatePath,
			schema,
			set(),
			REPOSITORY_ROOT,
			False,
		)

		self.assertIsNotNone(proposal)
		self.assertEqual(errors, [])

	def testSchemaRequiredFieldsControlValidation(self):
		schema = self.loadSchema()
		proposal = self.loadTemplate()
		changedSchema = copy.deepcopy(schema)
		changedSchema["required"].append("reviewNote")
		changedSchema["properties"]["reviewNote"] = {
			"type": "string",
			"minLength": 1,
		}
		errors = []

		validator.validateSchemaValue(proposal, changedSchema, "proposal", errors)

		self.assertIn("proposal: missing required property 'reviewNote'", errors)

	def testAiAssistedModeRequiresSystemDisclosure(self):
		schema = self.loadSchema()
		proposal = self.loadTemplate()
		proposal["authorship"]["mode"] = "agent_drafted_human_reviewed"
		errors = []

		validator.validateSchemaValue(proposal, schema, "proposal", errors)
		validator.validateAuthorship(proposal, "proposal", errors)

		self.assertIn(
			"proposal.authorship.aiSystems: this authorship mode requires at least one AI system",
			errors,
		)

	def testRepositoryPathCannotEscape(self):
		errors = []

		result = validator.resolveRepositoryPath(
			"../outside.md",
			REPOSITORY_ROOT,
			"proposal.affectedProvisions[0]",
			errors,
		)

		self.assertIsNone(result)
		self.assertEqual(len(errors), 1)


if __name__ == "__main__":
	unittest.main()
