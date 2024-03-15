async function imageGen(params){
    const {prompt, aspect_ratio, num_images, model} = params;

    const response = await fetch("FUNCTION_URL", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": "YOUR API KEY"
        },
        body: JSON.stringify({"prompt": prompt, "aspect_ratio": aspect_ratio, "num_images": num_images, "model": model})
    });

    return response.json();
}