# picture-auth
 Improvement of machine learning image generation technologies, those such as Midjourney, will likely lead to increased uncertainty of the provenance of digital media. Fake imagery and video may allow for manipulation of public perception.

 NOSTR, and its utlization of public / private key pairs, may offer a unique way to assert ownership of digital imagery. Also, the decentralized nature of NOSTR also keeps intact anonymity for those that wish to assert validity or ownership while preserving privacy. 

 This simple project offers a way of embedding a public key (npub) and the hashed private key [SHA256(nsec)] into a jpeg image. The embedded data can then be extracted.

 # Future work
 The next step is construct a simple UI to login with NOSTR credentials, embed data, and store the new image locally. Following successful login flow, leverage an onboard camera to capture images and embed metatdata "on-click."

 As of now, the end goal is development of a NOSTR app for use on an iPhone that allows for the capture and local storage of metadata-embedded digital imagery. 
