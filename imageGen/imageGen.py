import json, os
import replicate
import requests
import threading
from openai import OpenAI

def sd_xl(event, context):
    try:
        try:
            try:
                body = event["body"]
                if type(body) == str:
                    body = json.loads(body)
            except:
                body = json.loads(event["body"])
            print("Trying to get values")
            prompt = body["prompt"]
            aspect_ratio = body["aspect_ratio"]
            num_images = body["num_images"]
            model = body["model"]
            print("Got Values")
        except Exception as e:
            rm_message = {"reason": "Incorrect Body."}
            return {
                'statusCode': 400,
                'body': json.dumps(rm_message)
            }
        
        if aspect_ratio == "square":
            height = 1024
            width = 1024
        elif aspect_ratio == "landscape":
            height = 768
            width = 1344
        elif aspect_ratio == "portrait":
            height = 1344
            width = 768
        else:
            height = 1024
            width = 1024
            
        if num_images == None:
            num_images = 1
        if num_images > 4:
            num_images = 4
        if num_images < 1:
            num_images = 1
            
        negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"
        
        client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY'))
        
        use_model = ""
        
        if model == "sd-xl-quick":
            use_model = "lucataco/sdxl-lightning-4step:727e49a643e999d602a896c774a0658ffefea21465756a6ce24b7ea4165eba6a"
        else: 
            use_model = "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
        
        try: 
            output = client.run(
                use_model,
                input={
                    "height": int(height),
                    "width": int(width),
                    "num_outputs": num_images,
                    "prompt": prompt,
                    "disable_safety_checker": True
                }
            )
            
            #output = ['https://replicate.delivery/pbxt/ADugPDTpXp6TP9fIaO1vbfh5aHrxCztrPBfYWkEtBtd5OnJkA/out-0.png']
            print(output)
            
            print("Got Images from Replicate")
            body = {"images": output}
            print("Build return body.")
            print(body)
            
            return {
                'statusCode': 200,
                'body': body
            }
        except:
            return {
                'statusCode': 400,
                'body': {"reason:": "Could not generate images. Try again later."}
            }
    except Exception as e:
        print(f"Error: {e}")  # Log the exception details
        return {
            'statusCode': 500,
            'body': json.dumps({"reason": f"Server Error!"})
        }

def open_dalle(event, context):
    try:
        try:
            try:
                body = event["body"]
                if type(body) == str:
                    body = json.loads(body)
            except:
                body = json.loads(event["body"])
            print("Trying to get values")
            prompt = body["prompt"]
            aspect_ratio = body["aspect_ratio"]
            num_images = body["num_images"]
            print("Got Values")
        except Exception as e:
            rm_message = {"reason": "Incorrect Body."}
            return {
                'statusCode': 400,
                'body': json.dumps(rm_message)
            }
        
        if aspect_ratio == "square":
            height = 1024
            width = 1024
        elif aspect_ratio == "landscape":
            height = 768
            width = 1344
        elif aspect_ratio == "portrait":
            height = 1344
            width = 768
        else:
            height = 1024
            width = 1024
            
        if num_images == None:
            num_images = 1
        if num_images > 4:
            num_images = 4
        if num_images < 1:
            num_images = 1
            
        negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"

        client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY'))

        try: 
            output = client.run(
                #"lucataco/open-dalle-v1.1:1c7d4c8dec39c7306df7794b28419078cb9d18b9213ab1c21fdc46a1deca0144",
                #"lucataco/proteus-v0.1:4cdc699d5bfc17e774e9ad11696075d68dc38dec1dbcbfba85c2bb040d3c5cfe",
                #"lucataco/proteus-v0.2:06775cd262843edbde5abab958abdbb65a0a6b58ca301c9fd78fa55c775fc019",
                #"lucataco/proteus-v0.3:b28b79d725c8548b173b6a19ff9bffd16b9b80df5b18b8dc5cb9e1ee471bfa48",
                "lucataco/proteus-v0.4:34a427535a3c45552b94369280b823fcd0e5c9710e97af020bf445c033d4569e",
                input={
                    "height": int(height),
                    "width": int(width),
                    "num_outputs": num_images,
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "disable_safety_checker": True
                }
            )
            
            print(output)
            
            print("Got Images from Replicate")
            body = {"images": output}
            print("Build return body.")
            print(body)
            
            return {
                'statusCode': 200,
                'body': body
            }
        except:
            return {
                'statusCode': 400,
                'body': {"reason:": "Could not generate images. Try again later."}
            }
    except Exception as e:
        print(f"Error: {e}")  # Log the exception details
        return {
            'statusCode': 500,
            'body': json.dumps({"reason": f"Server Error!"})
        }

def playground_v2(event, context):
    try:    
        try:
            try:
                body = event["body"]
                if type(body) == str:
                    body = json.loads(body)
            except:
                body = json.loads(event["body"])
            print("Trying to get values")
            prompt = body["prompt"]
            aspect_ratio = body["aspect_ratio"]
            num_images = body["num_images"]
            print("Got Values")
        except Exception as e:
            rm_message = {"reason": "Incorrect Body."}
            return {
                'statusCode': 400,
                'body': json.dumps(rm_message)
            }
        
        if aspect_ratio == "square":
            height = 1024
            width = 1024
        elif aspect_ratio == "landscape":
            height = 768
            width = 1344
        elif aspect_ratio == "portrait":
            height = 1344
            width = 768
        else:
            height = 1024
            width = 1024
            
        if num_images == None:
            num_images = 1
        if num_images > 4:
            num_images = 4
        if num_images < 1:
            num_images = 1
            
        negative_prompt = "ugly, deformed, noisy, blurry, distorted, out of focus, bad anatomy, extra limbs, poorly drawn face, poorly drawn hands, missing fingers"
        
        try: 
            def generate_image(client, prompt, height, width, output_list):
                output = client.run(
                    #"playgroundai/playground-v2-1024px-aesthetic:42fe626e41cc811eaf02c94b892774839268ce1994ea778eba97103fe1ef51b8",
                    "lucataco/playground-v2.5-1024px-aesthetic:419269784d9e00c56e5b09747cfc059a421e0c044d5472109e129b746508c365",
                    input={
                        "height": int(height),
                        "width": int(width),
                        "num_outputs": 1,
                        "prompt": prompt,
                        "disable_safety_checker": True
                    }
                )
                if output:
                    output_list.extend(output)  # Thread-safe operation
            
            def generate_images(prompt, num_images, height, width):
                client = replicate.Client(api_token=os.getenv('REPLICATE_API_KEY')) 
                threads = []
                total_output = []  # Shared list to store results
            
                for _ in range(num_images):
                    thread = threading.Thread(target=generate_image, args=(client, prompt, height, width, total_output))
                    threads.append(thread)
                    thread.start()
            
                for thread in threads:
                    thread.join()  # Wait for all threads to complete
            
                return total_output
                
            total_output = generate_images(prompt, num_images, height, width)
            
            print("Got Images from Replicate")
            body = {"images": total_output}
            print("Build return body.")
            print(body)
            
            return {
                'statusCode': 200,
                'body': body
            }
        except:
            return {
                'statusCode': 400,
                'body': {"reason:": "Could not generate images. Try again later."}
            }
    except Exception as e:
        print(f"Error: {e}")  # Log the exception details
        return {
            'statusCode': 500,
            'body': json.dumps({"reason": f"Server Error"})
        }

def dalle(event, context):
    try:
        try:
            body = event["body"]
            if type(body) == str:
                body = json.loads(body)
        except:
            body = json.loads(event["body"])
        print("Trying to get values")
        prompt = body["prompt"]
        aspect_ratio = body["aspect_ratio"]
        num_images = body["num_images"]
        model = body["model"]
        print("Got Values")
    except Exception as e:
        rm_message = {"reason": "Incorrect Body."}
        return {
            'statusCode': 400,
            'body': json.dumps(rm_message)
        }
        
    if aspect_ratio == "square":
        height = 1024
        width = 1024
    elif aspect_ratio == "landscape":
        height = 1024
        width = 1792
    elif aspect_ratio == "portrait":
        height = 1792
        width = 1024
    else:
        height = 1024
        width = 1024
        
    image_size = str(width)+"x"+str(height)
        
    if num_images == None:
        num_images = 1
    if num_images > 4:
        num_images = 4
    if num_images < 1:
        num_images = 1
        
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
        
        image_url = response.data[0].url
        print(image_url)
        
        body = {'images': json.dumps(image_url)}
    except:
        return {
            'statusCode': 400,
            'body': 'Error generating images, try again later.'
        }
        

def lambda_handler(event, context):
    try: 
        if event["headers"]["x-api-key"] != os.getenv('SERVICE_API_KEY'):
            print("Wrong api key!")
            return {
                'statusCode': 401
            }
        else:
            #return event
            
            try:
                try:
                    body = event["body"]
                    if type(body) == str:
                        body = json.loads(body)
                except:
                    body = json.loads(event["body"])
                    
                print(str(body))
                if body["model"] == "sd-xl" or body["model"] == "sd-xl-quick":
                    return sd_xl(event, context)
                elif body["model"] == "open-dalle":
                    return open_dalle(event, context)
                elif body["model"] == "playground-v2":
                    return playground_v2(event, context)
                elif body["model"] == "dall-e-3" or body["model"] == "dall-e-3-hd":
                    return dalle(event, context)
                else:
                    print("Model not found!")
                    return {
                        'statusCode': 404,
                        'body': json.dumps({"reason": "Model not Found"})
                    }
            except:
                print("Model not found!" + str(body))
                return {
                        'statusCode': 404,
                        'body': json.dumps({"reason": "Model not Found"})
                    }
    except:
        return {
                'statusCode': 500
            }