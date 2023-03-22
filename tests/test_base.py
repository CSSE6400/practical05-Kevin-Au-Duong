import unittest
from tfparse import load_from_path


REQUIRED_PROVIDER = {
    "required_providers": {
        "aws": {
            "source": "hashicorp/aws",
            "version": "~> 4.0"
        }
    }
}

PROVIDER = {
    "provider": [
        {
            "region": "us-east-1",
            "shared_credentials_files": ["./credentials"]
        }
    ]
}

class TestTerraform(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tf = load_from_path(".")

    def assertResource(self, resource, expected):
        for key, value in expected.items():
            if isinstance(value, dict):
                self.assertResource(resource[key], value)
            elif isinstance(value, list):
                self.assertResourceList(resource[key], value)
            else:
                self.assertIn(key, resource)
                self.assertEqual(resource[key], value)

    def assertResourceList(self, resource_list, expected):
        self.assertEqual(len(resource_list), len(expected), "Wrong number of resources")
        for resource, expected in zip(resource_list, expected):
            if isinstance(expected, dict):
                self.assertResource(resource, expected)
            else:
                self.assertEqual(resource, expected)

    def resource_by_name(self, resource_list, name):
        for resource in resource_list:
            if resource["__tfmeta"]["path"] == name:
                return resource
        return None


class TestProvider(TestTerraform):
    def test_required_provider(self):
        self.assertIn("terraform", self.tf, "No terraform block found")
        terraform = self.tf["terraform"][0]
        self.assertResource(terraform, REQUIRED_PROVIDER)
   
    def test_provider(self):
        self.assertResource(self.tf, PROVIDER)

        provider = self.tf["provider"][0]
        self.assertEqual(provider["__tfmeta"]["label"], "aws", "Wrong provider")
    
