$body = @{
    client_id = "106601"
    client_secret = "bc1a5db538ceeb56e96ca8b8560d242fe23db32d"
    code = "869161d871ed46862fe97e635fa01fd4b8239c84"
    grant_type = "authorization_code"
}

Invoke-RestMethod -Uri "https://www.strava.com/oauth/token" -Method Post -Body $body
