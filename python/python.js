async function python(params){
    const {code, packages} = params;

    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 90000); // 1m 30s timeout

    const response = await Promise.race([
        fetch("FUNCTION URL", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": "YOUR API KEY"
            },
            body: JSON.stringify({"code": code}),
            signal: controller.signal
        }),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timed out')), 90000)
        )
    ]);

    clearTimeout(id);

    return response.json();
}