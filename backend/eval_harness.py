import requests 

API_URL = "http://127.0.0.1:8000"

TEST_QUESTIONS = [
    {
        "question": "What problem does the Ford-Fulkerson algorithm solve?",
        "must_contain": ["ford-fulkerson", "flow"]
    },
    {
        "question": "What does it mean for two functions to grow at the same asymptotic rate?",
        "must_contain": ["asymptotic", "common factor"]
    },
    {
        "question": "How does the divide and conquer approach solve the maximum subarray problem?",
        "must_contain": ["maximum subarray", "divide"]
    },
    {
        "question": "What is the recurrence for integer multiplication?",
        "must_contain": ["integer multiplication", "t(n)"]
    },
    {
        "question": "What is the rod cutting problem?",
        "must_contain": ["rod cutting"]
    },
    {
        "question": "How is the longest common subsequence problem solved?",
        "must_contain": ["longest common subsequence", "lcs"]
    },
    {
        "question": "How are Huffman codes constructed?",
        "must_contain": ["huffman", "prefix code", "preﬁx code", "frequency"]
    },
    {
        "question": "What is depth first search used for?",
        "must_contain": ["depth first search", "dfs"]
    },
    {
        "question": "How does an algorithm find a minimum spanning tree?",
        "must_contain": ["minimum spanning tree", "mst"]
    },
    {
        "question": "How does Dijkstra's algorithm find shortest paths?",
        "must_contain": ["dijkstra"]
    },
    {
        "question": "What problem does the Bellman-Ford algorithm solve?",
        "must_contain": ["bellman-ford", "bellman ford"]
    },
    {
        "question": "What does the Floyd-Warshall algorithm compute?",
        "must_contain": ["floyd-warshall", "floyd warshall"]
    },
    {
        "question": "What is the maximum flow problem?",
        "must_contain": ["maximum flow", "max flow"]
    },
]

def run_single_test(test_case, n_results=4):
    response = requests.get(
        f"{API_URL}/ask-pdf",
        params={"question": test_case["question"], "n_results": n_results}
    )

    if response.status_code != 200:
        return {
            "question": test_case["question"],
            "passed": False,
            "reason": f"HTTP error {response.status_code}"
        }
    
    data = response.json()

    if "error" in data:
        return {
            "question": test_case["question"],
            "passed": False,
            "reason": f"Backend error: {data['error']}"
        }
    
    retrieved_text = " ".join(data["retrieved_chunks"]).lower()

    found = any(keyword in retrieved_text for keyword in test_case["must_contain"])

    return {
        "question": test_case["question"],
        "passed": found,
        "reason": "Keyword found" if found else "No matching keyword in retrieved chunks",
        "retrieved_preview": retrieved_text[:200]
    }

def run_all_tests():
    results = []

    for test_case in TEST_QUESTIONS:
        result = run_single_test(test_case)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {result['question']}")

        if not result["passed"]:
            print(f"  Reason: {result['reason']}")
            print(f"  Retrieved Preview: {result['retrieved_preview']}")

    return results

def print_summary(results):
    total = len(results)
    passed = sum(1 for r in results if r["passed"])

    print("\n--- Summary ---")
    print(f"Passed: {passed}/{total} ({passed / total * 100:.1f}%)")

if __name__ == "__main__":
    results = run_all_tests()
    print_summary(results)