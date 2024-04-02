async function wolfram(params, userSettings){
    const {query} = params;

    const response = await fetch(userSettings.functionURL, {
        method: "POST",
        mode: "cors",
        headers: {
            "x-api-key": userSettings.apiKey
        },
        body: JSON.stringify({"query": query})
    });

    response_text = await response.text();

    // Find the "output" key in the response
    markdown_data = "**Query:**\n```markdown\n" + query + "\n```\n" + "**Output:**\n```markdown\n" + response_text + "\n```";

    return {
        _TM_CUSTOM_OUTPUT: true,
        type: 'markdown',
        data: markdown_data,
        response: response_text 
    }
}