async function python(params, userSettings){
    const {code, packages} = params;

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
            body: JSON.stringify({"code": code}),
            signal: controller.signal
        }),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timed out')), 90000)
        )
    ]);

    clearTimeout(id);

    response_json = await response.json();

    // Find the "output" key in the response
    markdown_data = response_json['output'];
    markdown_data = "**Code:**\n```python\n" + code + "\n```\n" + "**Output:**\n```markdown\n" + markdown_data + "\n```";

    return {
        _TM_CUSTOM_OUTPUT: true,
        type: 'markdown',
        data: markdown_data,
        response: response_json 
    }
}