def evaluate_workflow_steps(
    state
):

    completed = True

    required_nodes = [

        "planner",

        "researcher",

        "critic",

        "synthesizer"
    ]

    for node in required_nodes:

        if node not in state:

            completed = False

    return completed