"""Independent dynamic programming examples."""


def knapsack_01(weights, values, capacity):
    if len(weights) != len(values) or capacity < 0 or any(w < 0 for w in weights): raise ValueError("Invalid knapsack input")
    dp = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1): dp[c] = max(dp[c], dp[c - weight] + value)
    return dp[capacity]


def lcs_length(first, second):
    row = [0] * (len(second) + 1)
    for a in first:
        current = [0]
        for j, b in enumerate(second, 1): current.append(row[j - 1] + 1 if a == b else max(row[j], current[-1]))
        row = current
    return row[-1]


def matrix_chain_order(dimensions):
    if len(dimensions) < 2 or any(d <= 0 for d in dimensions): raise ValueError("Provide at least two positive dimensions")
    n = len(dimensions) - 1; dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = min(dp[i][k] + dp[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1] for k in range(i, j))
    return dp[0][n - 1]


def resource_allocation(returns, budget):
    """Maximize return across projects. returns[i][b] is project i's return at integer allocation b; allocations sum to budget."""
    if budget < 0 or any(len(row) <= budget for row in returns): raise ValueError("Each project row must cover allocations 0..budget")
    dp = [0] * (budget + 1)
    for row in returns:
        nxt = [float("-inf")] * (budget + 1)
        for spent in range(budget + 1):
            for allocated in range(spent + 1): nxt[spent] = max(nxt[spent], dp[spent - allocated] + row[allocated])
        dp = nxt
    return dp[budget]
