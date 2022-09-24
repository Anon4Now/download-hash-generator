# Hash Generator

I created this tool because I wanted an easier way to evaluate downloads that I was making online.

A lot of good sites provide the hashes that are attributed to their offical copy of the product, however that hash is only as good as the user who recreates it after download. This tool will automate that process of generating the hashes and makes it easier to compare to the hash value on the download site. Additionally this tool has a module that will call a VirusTotal API and check to see if a this hash was evaluated before, and if so it will return those findings.

## Tool Functionality:

- Will use a "watchdog" function to monitor a path defined by the user, it will default to the OS's "Download" folder
- Will generate SHA256, SHA1, and MD5 hashes for a file, this is done because some sites provide only one of those options
- Can provide the ability to take the SHA256 hash and check VirusTotal's scanned database of files (read on for how to enable this functionality)

## Tool Requirements:

- To use the default functionality of this tool (watching folders, and creating hashes) a couple of modules will need to be installed using pip
  - [watchdog](https://pypi.org/project/watchdog/)
  - [dotenv](https://pypi.org/project/python-dotenv/)
- To use the VirusTotal API functionality, it will require an VT account and API key
  - Use this article [LINK](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1) to learn more about .env and this [LINK](https://www.tines.com/blog/virustotal-api-security-automation) for VT account creation (it's easy honestly)
  - Afterwards progress to IMPORTANT section below for information about what to do with the API key
- Lastly this tool needs a ![small](https://user-images.githubusercontent.com/80045938/148561762-9590c4a1-a424-4c7b-a0fb-68190fb7a31c.png) [Python](https://www.python.org/downloads/) interpreter, v3.6 or higher due to string interpolation

## Quick Notes:

- This can be converted to a standalone exe if run on Windows OS
- This tool will work regardless of whether the API functionality is set-up, the prompt to run against VT will not appear
- This should work on Linux, OSX, or Windows OS's
- This can be tested with any file that can be downloaded (🟨 NOTE: if downloading something as large as a VM, the results may not be correct)

## Resource Path:

````
rootdir:.
│   .gitignore
│   config.json
│   main.py
│   README.md
│   requirements.txt
│
├───resources
│   │   errors.py
│   │   hash_generator.py
│   │   user_prompts.py
│   │   utils.py
│   │   vt_check.py
│   │   __init__.py
│
├───tests
│   │   test_hash_generator.py
│   │   test_main.py
│   │   test_user_prompts.py
│   │   test_vt_check.py
│   │   __init__.py
│   │
│   ├───json_files
│   │       no_results.json
│   │       results.json
```it

## ❗IMPORTANT:

This tool will hide the prompt to take the generated SHA256 hash unless the user has created a .env file in the same directory as the source files. This is done to prevent the user from attempting to hard code their API credentials into the code, and to do it the secure way through leveraging environment variables.

Obviously I cannot stop anyone from taking that route if they really want, but I would strongly suggest against it. Creating and using environment variables for this tool is easy. For more information on how to create a .env file, use this [LINK](https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1).

Once you have created the .env file in the correct directory update the file with the variables below, reference the VirusTotal's API [DOCS](https://developers.virustotal.com/reference/overview) for more info:

````

# Development settings

API_ENDPOINT=https://www.virustotal.com/api/v3/files/
API_KEY="x-apikey"
API_KEY_VAL="<API_KEY_VAL>"

```

At this point you are done, and the prompt "_Would you like to check the SHA256 hash against VirusTotal DB? [y/n] >>_" should appear after you generate hashes.

## Using the Tool:

#### Step 1:

Run the binary or standalone exe to start CLI prompts.
![start_program](https://user-images.githubusercontent.com/80045938/149607071-48f9168b-bf46-4245-8994-ad9e01adc7a8.gif)

#### Step 2:

Download the wanted file, the program will generate SHA256, SHA1, and MD5 hashes. This will take approximately 8-10 seconds.
![gen_hashes](https://user-images.githubusercontent.com/80045938/149607081-1050a921-d786-4da3-bd5d-85ec620862b6.gif)

#### Step 3:

**IMPORTANT** For this option to be presented to the user, a .env file will need to be present
![get_api_results](https://user-images.githubusercontent.com/80045938/149607147-1d7fe82a-d119-460e-9203-f9471e3a9342.gif)
```
