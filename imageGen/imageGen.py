import json
import os
import replicate
from openai import OpenAI
import threading

def sd_xl(event, context):
    try:
        body = json.loads(event["body"])
        prompt = body["prompt"]
        aspect_ratio = body["aspect_ratio"]
        num_images = body["num_images"]
        model = body["model"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Incorrect Body."})
        }

    # Set image dimensions based on aspect ratio
    if aspect_ratio == "square":
        height, width = 1024, 1024
    elif aspect_ratio == "landscape":
        height, width = 768, 1344
    elif aspect_ratio == "portrait":
        height, width = 1344, 768
    else:
        height, width = 1024, 1024

    # Ensure num_images is within the valid range
    if num_images is None:
        num_images = 1
    else:
        num_images = max(1, min(int(num_images), 4))

    negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"

    client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY'))

    # Choose the appropriate model based on the input
    if model == "sd-xl-quick":
        model_id = "lucataco/sdxl-lightning-4step:727e49a643e999d602a896c774a0658ffefea21465756a6ce24b7ea4165eba6a"
    else:
        model_id = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"

    try:
        output = client.run(
            model_id,
            input={
                "height": height,
                "width": width,
                "num_outputs": num_images,
                "prompt": prompt,
                "disable_safety_checker": True
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({"images": output})
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Could not generate images. Try again later."})
        }

def open_dalle(event, context):
    try:
        body = json.loads(event["body"])
        prompt = body["prompt"]
        aspect_ratio = body["aspect_ratio"]
        num_images = body["num_images"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Incorrect Body."})
        }

    # Set image dimensions based on aspect ratio
    if aspect_ratio == "square":
        height, width = 1024, 1024
    elif aspect_ratio == "landscape":
        height, width = 768, 1344
    elif aspect_ratio == "portrait":
        height, width = 1344, 768
    else:
        height, width = 1024, 1024

    # Ensure num_images is within the valid range
    if num_images is None:
        num_images = 1
    else:
        num_images = max(1, min(int(num_images), 4))

    negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"

    client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY'))

    try:
        output = client.run(
            "lucataco/proteus-v0.4:34a427535a3c45552b94369280b823fcd0e5c9710e97af020bf445c033d4569e",
            input={
                "height": height,
                "width": width,
                "num_outputs": num_images,
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "disable_safety_checker": True
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({"images": output})
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Could not generate images. Try again later."})
        }

def playground_v2(event, context):
    try:
        body = json.loads(event["body"])
        prompt = body["prompt"]
        aspect_ratio = body["aspect_ratio"]
        num_images = body["num_images"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Incorrect Body."})
        }

    # Set image dimensions based on aspect ratio
    if aspect_ratio == "square":
        height, width = 1024, 1024
    elif aspect_ratio == "landscape":
        height, width = 768, 1344
    elif aspect_ratio == "portrait":
        height, width = 1344, 768
    else:
        height, width = 1024, 1024

    # Ensure num_images is within the valid range
    if num_images is None:
        num_images = 1
    else:
        num_images = max(1, min(int(num_images), 4))

    negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"

    def generate_image(client, prompt, height, width, output_list):
        output = client.run(
            "lucataco/playground-v2.5-1024px-aesthetic:419269784d9e00c56e5b09747cfc059a421e0c044d5472109e129b746508c365",
            input={
                "height": height,
                "width": width,
                "num_outputs": 1,
                "prompt": prompt,
                "disable_safety_checker": True
            }
        )
        if output:
            output_list.extend(output)

    def generate_images(prompt, num_images, height, width):
        client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY'))
        threads = []
        total_output = []

        for _ in range(num_images):
            thread = threading.Thread(target=generate_image, args=(client, prompt, height, width, total_output))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return total_output

    total_output = generate_images(prompt, num_images, height, width)
    return {
        'statusCode': 200,
        'body': json.dumps({"images": total_output})
    }

def dalle(event, context):
    try:
        body = json.loads(event["body"])
        prompt = body["prompt"]
        aspect_ratio = body["aspect_ratio"]
        num_images = body["num_images"]
        model = body["model"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Incorrect Body."})
        }

    # Set image dimensions based on aspect ratio
    if aspect_ratio == "square":
        height, width = 1024, 1024
    elif aspect_ratio == "landscape":
        height, width = 1024, 1792
    elif aspect_ratio == "portrait":
        height, width = 1792, 1024
    else:
        height, width = 1024, 1024

    image_size = f"{width}x{height}"

    # Ensure num_images is within the valid range
    if num_images is None:
        num_images = 1
    else:
        num_images = max(1, min(int(num_images), 4))

    # Set the quality based on the model
    if model == "dall-e-3-hd":
        quality = "hd"
    elif model == "dall-e-3":
        quality = "standard"
    else:
        quality = "standard"

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=image_size,
            quality=quality,
            n=num_images,
        )
        image_url = [item.url for item in response.data]
        return {
            'statusCode': 200,
            'body': json.dumps({"images": image_url})
        }
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"reason": "Error generating images, try again later."})
        }

def lambda_handler(event, context):
    try:
        if event["headers"]["x-api-key"] != os.getenv('SERVICE_API_KEY'):
            return {'statusCode': 401}

        body = json.loads(event["body"])
        model = body.get("model")

        if model == "sd-xl" or model == "sd-xl-quick":
            return sd_xl(event, context)
        elif model == "open-dalle":
            return open_dalle(event, context)
        elif model == "playground-v2":
            return playground_v2(event, context)
        elif model == "dall-e-3" or model == "dall-e-3-hd":
            return dalle(event, context)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({"reason": "Model not Found"})
            }
    except:
        return {
            'statusCode': 500
        }