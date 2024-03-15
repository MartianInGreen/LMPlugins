async function youtube(params){
    const {video_id} = params;

    // Make request to the server
    const response = await fetch("FUNCTION URL", {
        method: "POST",
        mode: "cors",
        body: JSON.stringify({"video_id": video_id})
    });

    return response.text();
}