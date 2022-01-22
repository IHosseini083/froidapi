
# TODOs 📝

Write your TODOs here and work on them without getting lost in your journey.

- [ ] Extract homepage applications.
- [ ] Extract the newest apps/games published on the farsroid.com.
- [ ] Add rate limiting to specific endpoints.
- [ ] Add more details in error responses.
- [ ] Add option for changing email.
- [ ] Add an option to restore the forgotten password.  
- [ ] Improve search functionality
  - [x] Add `/legacy/` path to search endpoint to get more details from search (description, thumbnail, etc.) but with much lower performance (slow data scraping, etc.)
- [ ] Parse a post's metadata from its download page

## In Progress 👨🏻‍💻

- [ ] Separate `media` and `related_posts` from ``/v1/posts/{post_id}`` response into different endpoints.
- [ ] Add request option to request new apps/games.
- [ ] Get apps/games by different categories

## Done ✅

- [x] Implement users registration
- [x] Add `APIKeyHeader` authentication for `/v1/posts/*` endpoints.
