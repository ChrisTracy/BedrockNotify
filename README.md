# BedrockNotify
A simple container to send a Discord notification based on Minecraft Bedrock logs. 
    
    docker run -d --restart unless-stopped --name bedrock-notify -e WEBHOOK="[webhookURL]" -e INTERVAL="20" -v /path/to/minecraft/server/logs:/MClogs christracy/bedrock-notify
