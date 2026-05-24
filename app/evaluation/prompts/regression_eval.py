def keyword_score(
    response,
    expected_keywords
):

    matches = 0

    for keyword in expected_keywords:

        if keyword.lower() in response.lower():

            matches += 1

    return matches / len(expected_keywords)