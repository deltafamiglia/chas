import asyncio

from components.agent.src.container.container_client import ContainerdClient


async def main():
    async with ContainerdClient() as client:
        # Pull image
        image_id = await client.pull_image("docker.io/library/redis:latest")

        # Create container
        container = await client.create_container(
            "redis-test",
            "docker.io/library/redis:latest",
            labels={"app": "redis"}
        )

        # Start container
        await container.start()

        # Get status
        status = await container.status()
        print(f"Container status: {status}")

        # List all containers
        containers = await client.list_containers()
        for c in containers:
            print(f"Found container: {c.id}")

        # Stop and delete container
        await container.stop(timeout=10)
        await container.delete()


if __name__ == "__main__":
    asyncio.run(main())

