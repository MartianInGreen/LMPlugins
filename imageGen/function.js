async function imageGen(params, userSettings){
    const {prompt, aspect_ratio, num_images, model} = params;

    const response = await fetch(userSettings.functionURL, {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": userSettings.apiKey
        },
        body: JSON.stringify({"prompt": prompt, "aspect_ratio": aspect_ratio, "num_images": num_images, "model": model})
    });

    return response.json();
}