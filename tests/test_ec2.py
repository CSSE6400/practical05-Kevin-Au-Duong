from tests.test_base import TestTerraform

EXPECTED_EC2 = {
    "ami": "ami-005f9685cb30f234b",
    "instance_type": "t2.micro",
    "key_name": "vockey",
    "user_data_replace_on_change": True,
    "security_groups": 
        {
            '__attributes__': ['aws_security_group.taskoverflow_instance.name']
        },
    "tags": {
        "Name": "taskoverflow_instance",
    }
}

EXPECTED_SECURITY_GROUP = {
    "name": "taskoverflow_instance",
    "description": "TaskOverflow Security Group",
    "ingress": [
        {
            "from_port": 6400,
            "to_port": 6400,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        }
    ],
    "egress":
        {
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }
}

class TestEC2(TestTerraform):
   
    def test_ec2_instance(self):
        self.assertIn("aws_instance", self.tf, "No aws_instance block found")
        instances = self.tf["aws_instance"]

        instance = self.resource_by_name(instances, "aws_instance.taskoverflow_instance")
        self.assertIsNotNone(instance, "No instance named taskoverflow_instance")

        self.assertResource(instance, EXPECTED_EC2)
        
    def test_ec2_sg(self):
        self.assertIn("aws_security_group", self.tf, "No aws_security_group block found")
        security_groups = self.tf["aws_security_group"]
        
        sg = self.resource_by_name(security_groups, "aws_security_group.taskoverflow_instance")
        self.assertIsNotNone(sg, "No security group named taskoverflow_instance")

        self.assertResource(sg, EXPECTED_SECURITY_GROUP)

