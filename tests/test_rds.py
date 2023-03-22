from tests.test_base import TestTerraform

EXPECTED_RDS = {
    "allocated_storage": 20,
    "max_allocated_storage": 1000,
    "engine": "postgres",
    "engine_version": "14",
    "instance_class": "db.t4g.micro",
    "db_name": "todo",
    "username": "administrator",
    "skip_final_snapshot": True,
    "vpc_security_group_ids":
        {
            '__attributes__': ['aws_security_group.taskoverflow_database.id']
        },
    "publicly_accessible": True,
    "tags": {
        "Name": "taskoverflow_database",
    }
}

EXPECTED_SECURITY_GROUP = {
    "name": "taskoverflow_database",
    "description": "Allow inbound Postgresql traffic",
    "ingress":
        {
            "from_port": 5432,
            "to_port": 5432,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    "egress":
        {
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }
}

class TestRDS(TestTerraform):
   
    def test_rds_instance(self):
        self.assertIn("aws_db_instance", self.tf, "No aws_db_instance block found")
        rds_instances = self.tf["aws_db_instance"]

        rds = self.resource_by_name(rds_instances, "aws_db_instance.taskoverflow_database")
        self.assertIsNotNone(rds, "No RDS instance named taskoverflow_database")

        self.assertResource(rds, EXPECTED_RDS)

    def test_rds_sg(self):
        self.assertIn("aws_security_group", self.tf, "No aws_security_group block found")
        sg = self.tf["aws_security_group"]

        sg = self.resource_by_name(sg, "aws_security_group.taskoverflow_database")
        self.assertIsNotNone(sg, "No security group named taskoverflow_database")

        self.assertResource(sg, EXPECTED_SECURITY_GROUP)

