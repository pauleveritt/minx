"""Demo from anyio."""

from anyio import sleep, create_task_group, run


async def some_task(num: int) -> None:  # noqa: D103
    print("Task", num, "running")
    await sleep(1)
    print("Task", num, "finished")


async def main() -> None:  # noqa: D103
    async with create_task_group() as tg:
        for num in range(5):
            tg.start_soon(some_task, num)

    print("All tasks finished!")


if __name__ == "__main__":
    run(main)
