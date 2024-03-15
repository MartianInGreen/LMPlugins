async function pondera(params){
    const {query, type, focus, country, freshness} = params;

    const response = await fetch("FUNCTION URL", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": "YOUR API KEY"
        },
        body: JSON.stringify({"query": query, "type": type, "focus": focus, "country": country, "freshness": freshness})
    });

    return response.json();
}