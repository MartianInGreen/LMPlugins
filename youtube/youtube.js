async function youtube(params, userSettings){
    const {video_id} = params;

    // Make request to the server
    const response = await fetch(userSettings.functionURL, {
        method: "POST",
        mode: "cors",
        body: JSON.stringify({"video_id": video_id})
    });

    return response.json();
}