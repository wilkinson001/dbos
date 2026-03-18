from dbos import ScheduleInput
from src.workflows import defend

WORKFLOWS: list[ScheduleInput] = [defend.BRONZE]
