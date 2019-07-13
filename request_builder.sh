#!/usr/bin/env bash
## To see information on registering clients  - https://developer.sas.com/reference/auth/#register
# consul_token = "25b1a976-4981-4b8b-97a1-c888ae89097a"


# REGISTERING CLIENTS
curl -X POST "http://dl-viya-cluster-1.dlviyacluster.sashq-r.openstack.sas.com/SASLogon/oauth/clients/consul?callback=false&serviceId=app" \
      -H "X-Consul-Token: 25b1a976-4981-4b8b-97a1-c888ae89097a"

#Response
{
    "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiJiNmRhZjk1N2YyZjc0MGIzYjY5MGU1M2E5NTIxOWQ5OSIsInN1YiI6InNhcy5hZG1pbiIsImF1dGhvcml0aWVzIjpbImNsaWVudHMucmVhZCIsImNsaWVudHMuc2VjcmV0IiwidWFhLnJlc291cmNlIiwiY2xpZW50cy53cml0ZSIsInVhYS5hZG1pbiIsImNsaWVudHMuYWRtaW4iLCJzY2ltLndyaXRlIiwic2NpbS5yZWFkIl0sInNjb3BlIjpbImNsaWVudHMuYWRtaW4iXSwiY2xpZW50X2lkIjoic2FzLmFkbWluIiwiY2lkIjoic2FzLmFkbWluIiwiYXpwIjoic2FzLmFkbWluIiwiZ3JhbnRfdHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsInJldl9zaWciOiJjNzYzOTZkZiIsImlhdCI6MTUyNTIzODcxNiwiZXhwIjoxNTI1MjgxOTE2LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImNsaWVudHMiLCJzYXMuKiIsInNhcy5hZG1pbiJdfQ.Szc_wqFAINfMPD6FYyAScL_5hUWQMr3K7NJVFixfj1MzhyOV39z5all3rJT4Ugvi2Wq9iD8xROwYy2WJWoKWwdQgp3SNvTH0hx6d0z191SAqz08i5STeg6WbndIjIb8Q0HLKcbwoKsfqaKRPctecg47KGyriKFFh1LHsR6g-9wg",
    "token_type": "bearer", "expires_in": 43199, "scope": "clients.admin", "jti": "b6daf957f2f740b3b690e53a95219d99"}


# USE THE VALUE OF THE ACCESS_TOKEN FIELD RETURNED IN THE RESPONSE JSON TO REGISTER THE NEW CLIENT
curl -X POST "http://dl-viya-cluster-1.dlviyacluster.sashq-r.openstack.sas.com/SASLogon/oauth/clients" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiJiNmRhZjk1N2YyZjc0MGIzYjY5MGU1M2E5NTIxOWQ5OSIsInN1YiI6InNhcy5hZG1pbiIsImF1dGhvcml0aWVzIjpbImNsaWVudHMucmVhZCIsImNsaWVudHMuc2VjcmV0IiwidWFhLnJlc291cmNlIiwiY2xpZW50cy53cml0ZSIsInVhYS5hZG1pbiIsImNsaWVudHMuYWRtaW4iLCJzY2ltLndyaXRlIiwic2NpbS5yZWFkIl0sInNjb3BlIjpbImNsaWVudHMuYWRtaW4iXSwiY2xpZW50X2lkIjoic2FzLmFkbWluIiwiY2lkIjoic2FzLmFkbWluIiwiYXpwIjoic2FzLmFkbWluIiwiZ3JhbnRfdHlwZSI6ImNsaWVudF9jcmVkZW50aWFscyIsInJldl9zaWciOiJjNzYzOTZkZiIsImlhdCI6MTUyNTIzODcxNiwiZXhwIjoxNTI1MjgxOTE2LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImNsaWVudHMiLCJzYXMuKiIsInNhcy5hZG1pbiJdfQ.Szc_wqFAINfMPD6FYyAScL_5hUWQMr3K7NJVFixfj1MzhyOV39z5all3rJT4Ugvi2Wq9iD8xROwYy2WJWoKWwdQgp3SNvTH0hx6d0z191SAqz08i5STeg6WbndIjIb8Q0HLKcbwoKsfqaKRPctecg47KGyriKFFh1LHsR6g-9wg" \
        -d '{
          "client_id": "app",
          "client_secret": "lnxsas",
          "scope": ["openid"],
          "authorized_grant_types": ["password"],
          "access_token_validity": 43199
         }'


#response

{"scope":["openid"],"client_id":"app","resource_ids":["none"],
"authorized_grant_types":["password","refresh_token"],"autoapprove":[],
"access_token_validity":43199,"authorities":["uaa.none"],"lastModified":1525240446184}


# OBTAINING ACCESS TOKENS WITH REGISTERED CLIENTS
curl -X POST "http://dl-viya-cluster-1.dlviyacluster.sashq-r.openstack.sas.com/SASLogon/oauth/token" \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "grant_type=password&username=viyademo01&password=lnxsas" \
      -u "app:lnxsas"


#response
{"access_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiJjMjg0MmU0NTk2ZjA0N2E0YTYxYmNiOWQzY2I3YTgyZSIsInN1YiI6IjUxNGJmZWEwLWM0MTgtNDQ0Zi1iMDA5LWVkYmE3ZGY3YmFmNCIsInNjb3BlIjpbIm9wZW5pZCJdLCJjbGllbnRfaWQiOiJhcHAiLCJjaWQiOiJhcHAiLCJhenAiOiJhcHAiLCJncmFudF90eXBlIjoicGFzc3dvcmQiLCJ1c2VyX2lkIjoiNTE0YmZlYTAtYzQxOC00NDRmLWIwMDktZWRiYTdkZjdiYWY0IiwiZXh0X2lkIjoidWlkPXZpeWFkZW1vMDEsb3U9dXNlcnMsZGM9dmE4MmRlbW8sZGM9Y29tIiwib3JpZ2luIjoibGRhcCIsInVzZXJfbmFtZSI6InZpeWFkZW1vMDEiLCJlbWFpbCI6InZpeWFkZW1vMDFAYW5zaWJsZS5kbHZpeWFjbHVzdGVyLnNhc2hxLXIub3BlbnN0YWNrLnNhcy5jb20iLCJhdXRoX3RpbWUiOjE1MjUyNzg0OTAsInJldl9zaWciOiJmZjIyMWYzZCIsImlhdCI6MTUyNTI3ODQ5MCwiZXhwIjoxNTI1MzIxNjg5LCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiYXVkIjpbImFwcCIsIm9wZW5pZCJdfQ.agotzYfLFM0-JVy24c8IIPQnr9B4YvowwgSauNHSllxUKIeMdNMVCAxdNI6Lw59sGEx0WvKJfdPuTDezXjPfEMXRuMGUWebl5cM-N8dyzSZ36HI3qo8GXyuaHI9GilVHjH8-6ighiAKnDZIr-eZrgOotbjA06eiiCZ0svtEExD4","token_type":"bearer","refresh_token":"eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiI0NDU5OTdlZTI3M2I0YWY2ODE0OTkzYjYxZDg2MDQ0ZS1yIiwic3ViIjoiNTE0YmZlYTAtYzQxOC00NDRmLWIwMDktZWRiYTdkZjdiYWY0Iiwic2NvcGUiOlsib3BlbmlkIl0sImlhdCI6MTUyNTI3ODQ5MCwiZXhwIjoxNTI3ODcwNDkwLCJjaWQiOiJhcHAiLCJjbGllbnRfaWQiOiJhcHAiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0L1NBU0xvZ29uL29hdXRoL3Rva2VuIiwiemlkIjoidWFhIiwiZ3JhbnRfdHlwZSI6InBhc3N3b3JkIiwidXNlcl9uYW1lIjoidml5YWRlbW8wMSIsIm9yaWdpbiI6ImxkYXAiLCJ1c2VyX2lkIjoiNTE0YmZlYTAtYzQxOC00NDRmLWIwMDktZWRiYTdkZjdiYWY0IiwiZXh0X2lkIjoidWlkPXZpeWFkZW1vMDEsb3U9dXNlcnMsZGM9dmE4MmRlbW8sZGM9Y29tIiwicmV2X3NpZyI6ImZmMjIxZjNkIiwiYXVkIjpbImFwcCIsIm9wZW5pZCJdfQ.bBg3DkGpeac1TLWXUo5qlUqK0J4hBAJYjv8Lu8Wb-f-Ib0vrQhqcQSj8gWj3U2RE1z27C4UWPF_kbRzy_r8OwC62gDsOXpRxVYMu7Y_MISY-4NYdSx0n-MO_8tajQByZYso1qskQpW-kDmEMAuAzy07qzWIpFhDHoIxfJSFvwvk",
"expires_in":43198,"scope":"openid","jti":"c2842e4596f047a4a61bcb9d3cb7a82e"}