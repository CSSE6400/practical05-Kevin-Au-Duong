from tests.test_base import TestTerraform

EXPECTED_CLUSTER = {
    "name": "taskoverflow"
}

EXPECTED_TASK_DEFINITION = {
    "family": "taskoverflow",
    "network_mode": "awsvpc",
    "requires_compatibilities": ["FARGATE"],
    "cpu": 1024,
    "memory": 2048,
    "execution_role_arn": {
        "__attribute__": 'data.aws_iam_role.lab.arn'
    },
}

EXPECTED_SERVICE = {
    "name": "taskoverflow",
    "cluster": {
        "__attribute__": 'aws_ecs_cluster.taskoverflow.id'
    },
    "task_definition": {
        "__attribute__": 'aws_ecs_task_definition.taskoverflow.arn'
    },
    "desired_count": 1,
    "launch_type": "FARGATE",

    "network_configuration": {
        "subnets": 
            {
                "__attribute__": 'data.aws_subnets.private.ids'
            },
        "security_groups":
            {
                "__attributes__": ['aws_security_group.taskoverflow.id']
            },
        "assign_public_ip": True
    },
}

EXPECTED_SECURITY_GROUP = {
    "name": "taskoverflow",
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

    def test_ecs_cluster(self):
        self.assertIn("aws_ecs_cluster", self.tf, "No aws_ecs_cluster block found")
        clusters = self.tf["aws_ecs_cluster"]

        cluster = self.resource_by_name(clusters, "aws_ecs_cluster.taskoverflow")
        self.assertIsNotNone(cluster, "No cluster named taskoverflow")

        self.assertResource(cluster, EXPECTED_CLUSTER)
 
    def test_ecs_task_definition(self):
        self.assertIn("aws_ecs_task_definition", self.tf, "No aws_ecs_task_definition block found")
        task_definitions = self.tf["aws_ecs_task_definition"]

        task_definition = self.resource_by_name(task_definitions, "aws_ecs_task_definition.taskoverflow")
        self.assertIsNotNone(task_definition, "No task definition named taskoverflow")

        self.assertResource(task_definition, EXPECTED_TASK_DEFINITION)

    def test_ecs_service(self):
        self.assertIn("aws_ecs_service", self.tf, "No aws_ecs_service block found")
        services = self.tf["aws_ecs_service"]

        service = self.resource_by_name(services, "aws_ecs_service.taskoverflow")
        self.assertIsNotNone(service, "No service named taskoverflow")

        self.assertResource(service, EXPECTED_SERVICE)

    def test_ecs_sg(self):
        self.assertIn("aws_security_group", self.tf, "No aws_security_group block found")
        security_groups = self.tf["aws_security_group"]
        
        sg = self.resource_by_name(security_groups, "aws_security_group.taskoverflow")
        self.assertIsNotNone(sg, "No security group named taskoverflow")

        self.assertResource(sg, EXPECTED_SECURITY_GROUP)

