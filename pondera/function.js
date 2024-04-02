async function pondera(params, userSettings){
    const {query, type, focus, country, freshness} = params;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 90000); // 1m 30s timeout

    const response = await Promise.race([
        fetch(userSettings.functionURL, {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": userSettings.apiKey
            },
            body: JSON.stringify({"query": query, "type": type, "focus": focus, "country": country, "freshness": freshness}),
            signal: controller.signal
        }),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timed out')), 90000)
        )
    ]);

    clearTimeout(id);

    return response.json();
}