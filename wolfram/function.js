async function wolfram(params){
    const {query} = params;

    const response = await fetch("FUNCTION_URL", {
        method: "POST",
        mode: "cors",
        headers: {
            "x-api-key": "YOUR API KEY"
        },
        body: JSON.stringify({"query": query})
    });

    return response.text();
}