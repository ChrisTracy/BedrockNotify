# BedrockNotify
A simple container to send a Discord notification based on Minecraft Bedrock logs. 
    
    docker run -d --restart unless-stopped --name bedrock-notify -e ALERTS="connected, disconnected" -e WEBHOOK="https://discord.com/api/webhooks/...." -e INTERVAL="10" -v /path/to/minecraft/logs:/MClogs christracy/bedrock-notify
