import os


def move_env_vars():
    """Переносит названия переменных окружения из .env в .env.dist без значений"""

    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    env_path = os.path.abspath(env_path)

    with open(env_path, "r") as env_file:
        sensetive_data = env_file.readlines()

    sensetive_data = list(filter(lambda line: line != "\n" and line[0] != ';', sensetive_data))

    clear_vars = "\n".join([line.split("=")[0] + "=" for line in sensetive_data])

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env.dist")), "w") as dist_file:
        dist_file.writelines(clear_vars)


if __name__ == "__main__":
    move_env_vars()
