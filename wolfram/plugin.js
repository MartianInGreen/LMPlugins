async function wolfram(params, userSettings) {
    const { query } = params;
    const appId = userSettings.appID;
    const displayOutput = userSettings.displayOutput;

    // Base URL for the Wolfram|Alpha API
    const baseURL = `https://www.wolframalpha.com/api/v1/llm-api?appid=${appId}&input=`;

    // Encode the query
    const encodedQuery = encodeURIComponent(query);
    const url = baseURL + encodedQuery;

    try {
        // Make the API request
        const response = await fetch(url);
        const data = await response.text();

        if (displayOutput) {
            // Format the output as Markdown
            const markdownData = `**Query:**\n\`\`\`markdown\n${query}\n\`\`\`\n**Output:**\n\`\`\`markdown\n${data}\n\`\`\``;

            return {
                _TM_CUSTOM_OUTPUT: true,
                type: 'markdown',
                data: markdownData,
                response: data
            };
        }else{
            return data
        }

        
    } catch (error) {
        console.error(error);
        return 'Error fetching Wolfram|Alpha results.'
    }
}