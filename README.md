# Sheltr
### TRY IT OUT: [sheltr.help](sheltr.help)
<img width="1718" alt="Screenshot 2025-04-20 at 23 13 39" src="https://github.com/user-attachments/assets/657f2f45-16c8-41e6-a1bb-0026b83e4882" />

### Demo: https://youtu.be/hMOs01PPEKY

## Inspiration
California is known for its frequent natural disasters, especially its wildfires during the latter half of the year. This year, we witnessed the L.A. fires that displaced tens of thousands of Californians. With only about 180 emergency call operators in L.A. County responsible for responding to several thousands of calls, response times can be delayed, which can put strain on emergency services. As natural disasters grow more severe due to climate change, our response must match the urgency. Therefore, we hoped to create an accessible and innovative solution to address this issue.

## What it does
Our platform is designed to provide quick access to shelter for those in need. When first entering our website/app, the user will instantly notice a filterable list of shelters in their area sorted based on distance. They also have access to shelter information including type, location, family accommodations, amenities, and more. Users can reserve spots for themselves and their families with just a phone number, ensuring they have a place secured. Once a reservation is made, users join a queue, and their spot is saved until they arrive, preventing overcrowding at shelters. Organizations and individuals wishing to provide shelter can create accounts to access a dashboard where they can post available shelters, track which users are checked in, and monitor live queue updates. Shelters from official organizations are verified, giving users confidence in the credibility of where they plan to stay.

## How we built it
Our website is hosted on AWS EC2 through NginX. The backend is designed through a FastAPI framework which has get, post, put, and delete requests. These requests are connected to an AWS DynamoDB database to store and update data of clients and shelters. Our front end is made simply through HTML, CSS, and JS. There is a user interface for users to find shelters and a client login and dashboard for shelter management. We also used Google’s Directions API and Geocode API to display the closest shelters based on driving distance for the user. Additionally, we use AWS Bedrock and Claude Haiku to summarize each shelter's ease of use.

## Challenges we ran into
A major challenge we ran into was when our API Keys weren’t responding, despite our implementations being correct. This was especially a problem with Google’s APIs, which continuously had issues. However, we tested different accounts and eventually overcame this problem. Another challenge we ran into was transferring data from users to shelters across Dynamo, as reservations and queue profiles had different data types. By cleaning up and reorganizing our code, we were able to diagnose what parts of the transfers the issues were at and could clear them up. This encouraged us to split our back-end among different files so that we could more easily diagnose errors and improve code readability.

## Accomplishments that we're proud of
Our team is proud to have made a solution to a problem that millions of California residents have faced over the past few years. Knowing that we created a tech-based solution to a problem that has directly impacted residents of our state, including our very own friends and family is encouraging and empowering. On the more technical side, we were proud of our use of AWS services, hosting our own website, creating a working log-in page, developing an easy-to-use UI, and leveraging powerful APIs to create the best solution to an extremely disturbing issue.

## What we learned
From this experience, we learned how to integrate complicated but modern technologies into our tech stack to ensure the fastest and most efficient way of processing, storing, and displaying data. Our group was able to hone our web and app development skills as well as the ability to host a website on AWS EC2. Lastly, we were able to implement APIs and troubleshoot errors regarding tokens.

## What's next for Sheltr
We have extremely bright hopes for Sheltr’s current and future impact on humanity and we are excited to expand our global reach. We want to expand our verification system so that clients can verify themselves using a form of identification. That way, users will feel the safety guarantee that Sheltr offers. We also hope to implement a review system where users are able to use a feedback button to rate/provide feedback on shelters. Given that we implemented modular and scalable code for our user and client database systems, this would be easily implemented into our preexisting project. This feedback would allow users to have more control and insight into where they are seeking refuge. The review system would help improve quality and accountability, as well as assist in the safety aspect as it’s some way of user verification of the shelters. We also believe that Sheltr could be a great tool for charitable distribution organizations. These organizations would use our client dashboard to direct resources to the shelters that need them the most. We created Sheltr simply for the benefit of people in need, and therefore we believe that Sheltr should run as a non-profit and would continue to run with funding for its hosting costs through donations and partnerships with charitable organizations.

## Built With
* amazon-dynamodb
* amazon-ec2
* bedrock
* claude
* nginx
* fastapi
* python
* google-maps
* html
* css
* javascript

Built with ❤️ by Thalen Abadia, Rahul Datta, Priyanka Ganguly, Rayyan Hussain, Aayush Kumbhare, Tommy Wickersham
