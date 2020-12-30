# API V1

Mounted on `/api/v1`.

Usage examples can be found by importing the `api_V1_postman.json` file into Postman.

## Table of contexts
1. [User entity](#user-entity)
2. [Event entity](#event-entity)
3. [Event comment entity](#event-comment-entity)
4. [Event invitation entity](#event-invitation-entity)
5. [User feedback entity](#user-feedback-entity)
5. [Paginated items](#paginated-items)
6. [User routes](#user-routes)
7. [Events routes](#events-routes)
8. [Event comments routes](#event-comments-routes)
9. [Event invitation routes](#event-invitation-routes)
10. [User feedback routes](#user-feedback-routes)

---

### User entity

This is how an user will be shown by the API.

```
{
    "first_name": "Admin",
    "last_name": "Name",
    "points": 10,
    "trust_level": 0,
    "username": "admin"
}
```

---

### Event entity

This is how an event will be shown by the API.

```
{
    "allows_more_participants": true,
    "category": 10,
    "category_text": "Music",
    "description": "Let's drink you fuckers",
    "end_time": "2021-11-30T15:19:59+00:00",
    "id": "5fca014590e774b63577ee4e",
    "is_limited_details": false,
    "is_unlimited_participants": false,
    "location": "Infinity, Piezisa",
    "location_points": [
        -25.0,
        32.0
    ],
    "location_points_radius_meters": null,
    "min_trust_level": 0,
    "no_max_participants": 10,
    "no_participants": 0,
    "owner": {
        "first_name": "Admin",
        "last_name": "Name",
        "points": 30,
        "trust_level": 0,
        "username": "admin"
    },
    "start_time": "2021-11-30T15:19:59+00:00",
    "title": "Beuta inf newnewnew",
    "visibility": 2,
    "visibility_text": "whitelisted"
}
```

`is_limited_details` shows whether some details are hidden from the user.

`allows_more_participants` shows whether more participants can join the event,
and is not available when `is_limited_details` is true. 

`location` represents the location of the event in text, and is not available when `is_limited_details` is true.

`location_points` represents location of the event in longitudinal and latitudinal coordinates. These coordinates are approximated when `is_limited_details` is true.

`location_points_radius_meters` represents the radius used when calculating the approximate location, and is only available when `is_limited_details` is true.

`no_participants` represents number of participants that currently have an accepted invitation to the event, and is not available when `is_limited_details` is true.

`no_max_participants` represents the number of max participants that can join the event, or 0 if an unlimited number of participants can join the event, and is not available when `is_limited_details` is true.

`is_unlimited_participants` is not available when `is_limited_details` is true.

---

### Event comment entity
```
{
    "author": {
        "first_name": "Admin",
        "last_name": "Name",
        "points": 30,
        "trust_level": 0,
        "username": "admin"
    },
    "id": "5fc42274fd571599a6cbd3a7",
    "text": "This is a comment for event 0",
    "time": "2020-11-30T00:36:36.519000"
}
```

---

### Event invitation entity
```
{
    "attend_status": 0,
    "attend_status_text": "unchecked",
    "id": "5fca1ff668b7ba795bbe5280",
    "status": 0,
    "status_text": "pending"
}
```

---

### User feedback entity
```
{
    "from_user": {
        "first_name": "Admin",
        "last_name": "Name",
        "points": 30,
        "trust_level": 0,
        "username": "admin"
    },
    "to_user": {
        "first_name": "Cosmin",
        "last_name": "Tanislav",
        "points": 0,
        "trust_level": 0,
        "username": "cosmin.tanislav"
    },
    "event": null,
    "points": 5,
    "message": "This dude rocked"
}
```

---

### Paginated items

This is how multiple items will be returned by the API.
The item is specific to each route.

#### Query parameters

`limit` is the number of items to return per-page, defaults to 100.

`page` is the index of the page, counting from 0, defaults to 0.

```
{
    "items": [
        {
            [... item properties ...]
        },
        [... more items ...]
        {
            [... item properties ...]
        }
    ],
    "limit": 5,
    "no_items": 5,
    "no_pages": 2,
    "no_total_items": 6,
    "page": 0,
    "skip": 0
}
```

`limit` is the limit specified using query parameters.

`page` is the page specified using query parameters.

`no_items` is the number of items on this page.

`no_pages` is the number of pages available.

`no_total_items` is the number of total items available.

`skip` is the calculated number of items skipped.

---

### User routes

#### `GET` `/user`

Return the user details of the logged in user.

##### Response body

See [User entity](#user-entity).

---

#### `POST` `/user/login`

Logs an user in, using the data provided in the request body.
Also, an access token cookie and a refresh token cookie are set.
The access token has a short expiration time and must be refreshed by using [this](#post-user-refresh).

##### Request body

```
{
    "username": "admin",
    "password": "pass"
}
```

##### Response body

See [User entity](#user-entity).

---

#### `POST` `/user/refresh`

Refreshes the access token cookie of the logged in user.

---

#### `POST` `/user/logout`

Logs out the logged in user, unsetting the access token cookie and the refresh token cookie.

---

#### `POST` `/user/register`

Registers a new user, using the data provided in the request body.

##### Request body

```
{
    "username": "cosmin.tanislav",
    "password": "test?",
    "first_name": "Cosmin",
    "last_name": "Tanislav"
}
```

##### Response body

See [User entity](#user-entity).

---

### Events routes

#### `GET` `/events/visibilities`

Return the available visibility types, to be used when creating an event.

##### Response body

```
{
    "public": 0,
    "unlisted": 1,
    "whitelisted": 2
}
```

---

#### `GET` `/events/categories`

Return the available categories, to be used when creating an event.

##### Response body

```
{
    "Arts": 0,
    "Book Clubs": 1,
    [... more properties ...]
    "Sport & Fitness": 14,
    "Tech": 15
}
```

---

#### `GET` `/events`

Return all events with either limited or full details.

An user can see whitelisted events with limited details.

An user can see public events with full details

A logged in user can see events that he owns with full details.

A logged in user can see events for which he has an accepted invite with full details.

##### Query parameters
`category` is the category to use when filtering. Can be specified multiple times to filter for multiple categories.

`invitation_status` is the invitation status to use when filtering. Can be specified multiple times to filter for multiple statuses. Only events for which the user has an invite with one of the given statuses will be shown.

`date_start` is the start of the interval to use when filtering. Only events starting after this date will be shown.

`date_end` is the end of the interval to use when filtering. Only events starting before this date will be shown.

##### Response body

See [Paginated items](#paginated-items) with [Event entity](#event-entity).


---

#### `POST` `/events`

Creates a new event with the logged in user as the owner.

##### Request body

```
{
    "title": "Beuta inf newnewnew",
    "location": "Infinity, Piezisa",
    "location_point": [-25.3465, 32.321312],
    "start_time": "2021-11-30T15:19:59+0000",
    "end_time": "2021-11-30T15:19:59+0000",
    "description": "Let's drink",
    "visibility": "whitelisted",
    "category": "Music",
    "min_trust_level": 1,
    "no_max_participants": 10
}
```

`location` is a textual representation of the location of the event.

`location_point` must be an array of 2 floating point numbers, used to describe the longitude and latitude of the location of the event.

See [here](#get-eventsvisibilities) for the `visibility` values.
Either numeric or string values can be used.

See [here](#get-eventscategories) for the `category` values.
Either numeric or string values can be used.

`start_time` must be after the current time.

`end_time` must be after the start time.

`min_trust_level` must be less or equal to the logged in user's trust level, but not less than zero. This property is optional and defaults to 0.

`no_max_participants` must not be less than zero.
Zero means that there's no limit to the number of participants that can join this event.
This property is optional and defaults to 0.

##### Response body

See [Event entity](#event-entity).

---

#### `GET` `/events/<string:event_id>`

Return an event with either limited or full details.

An user can see a whitelisted event with limited details.

An user can see a public event with full details.

A logged in user can see an unlisted event with limited details. Since an unlisted events are not visible within the events route, this means that the owner needs to share the link to it with people that he wants to let join.

A logged in user can see a whitelisted or unlisted event for which he has an accepted invite with full details.

A logged in user can see events that he owns with full details.

##### Response body

See [Event entity](#event-entity).

---

#### `PATCH` `/events/<string:event_id>`

Modify an event.

Only accessible for the owner of the event.

##### Request body

Same as [here](#post-events), but all properties are optional.
Properties not present will not be modified.

##### Response body

See [Event entity](#event-entity).

---

#### `DELETE` `/events/<string:event_id>`

Delete an event.

Only accessible for the owner of the event.

##### Response body

See [Event entity](#event-entity).

---

### Event comments routes

#### `GET` `/events/<string:event_id>/comments`

Return the comments for an event.

Any logged in user can see the comments of an event.

##### Response body

See [Paginated items](#paginated-items) with [Event comment entity](#event-comment-entity).

---

#### `POST` `/events/<string:event_id>/comments`

Create a comment for an event with the logged in user as the author.

Any logged in user can create a comment for an event.

##### Request body
```
{
    "text": "This is a comment"
}
```

##### Response body

See [Event comment entity](#event-comment-entity).

---

#### `PATCH` `/events/<string:event_id>/comments/<string:comment_id>`

Modify a comment.

Only accessible for the author of the comment.

##### Request body

Same as [here](#post-eventsstringevent_idcomments), but all properties are optional.
Properties not present will not be modified.

##### Response body

See [Event comment entity](#event-comment-entity).

---

#### `DELETE` `/events/<string:event_id>/comments/<string:comment_id>`

Delete a comment

Only accessible for the author of the comment.

##### Response body

See [Event comment entity](#event-comment-entity).

---

### Event invitation routes

#### `GET` `/events/invitation_statuses`

Return the available invitation statuses, to be used when modifying an invitation.

##### Response body

```
{
    "accepted": 1,
    "denied": 2,
    "pending": 0
}
```

#### `GET` `/events/invitation_attend_statuses`

Return the available invitation attendance statuses, to be used when modifying an invitation.

##### Response body

```
{
    "attended": 1,
    "missed": 2,
    "unchecked": 0
}
```


#### `GET` `/events/<string:event_id>/invitation`

Return the invitation for an event for the logged in user.

##### Response body

See [Event invitation entity](#event-invitation-entity).

---

#### `PUT` `/events/<string:event_id>/invitation`

Create an invitation for an event for the logged in user.

##### Response body

See [Event invitation entity](#event-invitation-entity).

---

#### `GET` `/events/<string:event_id>/invitations`

Return the invitations for an event.

A logged in user can see the accepted invitations for an event for which he has an accepted invite.

A logged in user can see all the invitations for an event that he owns.

##### Response body

See [Paginated items](#paginated-items) with [Event invitation entity](#event-invitation-entity).

---

#### `PATCH` `/events/<string:event_id>/invitations/<string:invitation_id>`

Modify an invitation.

Only accessible for the author of the event.

##### Request body

```
{
    "status": "accepted",
    "attend_status": "missed"
}
```

See [here](#get-invitation-statuses) for the `status` values.
Either numeric or string values can be used.

See [here](#get-invitation-attend-statuses) for the `attend_status` values.
Either numeric or string values can be used.

##### Response body

See [Event invitation entity](#event-invitation-entity).

---

### User feedback routes

#### `GET` `/feedbacks`

Return the feedback given to an user.

##### Query parameters

`to_user` represents the username of the user.

`event_id` represents the id of the event, optional.

##### Response body

See [User feedback entity](#user-feedback-entity).

---

#### `PUT` `/feedbacks`

Create or update a feedback for an user's activity, either at this particular event, if specified, or in general.

##### Query parameters

`to_user` represents the username of the user.

`event_id` represents the id of an event, optional.

##### Request body
```
{
    "points": 5,
    "message": " This guy rocks"
}
```

`points` represents the number of points that should be given to this user.

`message` represents a message to associate with the feedback, optional.

##### Response body

See [User feedback entity](#user-feedback-entity).
