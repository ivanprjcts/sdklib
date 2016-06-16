Feature: Sdklib samples
  # Enter feature description here

  Scenario: Try to pair a Latch application using an invalid pairing token
    # Enter steps here
    Given The API endpoint "https://latch.elevenpaths.com"
      #And The API proxy "http://localhost:8080"
      And The parameterized API resource "/api/%(version)s/pair/%(pairing_code)s" with these parameter values
       | key           | value   |
       | version       | 1.0     |
       | pairing_code  | 123456  |
      And 11Paths-Authorization with application id "nBDbNL8Ae7uzyZhvYNyg" and secret "UNz4fpbTNJcvPPQL8vYwgtZChMgdnNyGH8DB2nie"
    When I send a HTTP "GET" request
    Then The HTTP status code should be "200"
     And The response body should be this JSON
       """
       {"error":{"code":206,"message":"Token not found or expired"}}
       """


  Scenario: Search Github repositories
    # Enter steps here
    Given The API endpoint "https://api.github.com"
      #And The API proxy "http://localhost:8080"
      And The parameterized API resource "/orgs/%(organization)s/repos" with these parameter values
       | key           | value   |
       | organization  | octokit |
      And The headers
       | header_name | header_value                     |
       | Accept      | application/vnd.github.v3+json   |
       | User-Agent  | Hello-Agent!                     |
    When I send a HTTP "GET" request
    Then The HTTP status code should be "200"


  Scenario: scenario 3
    # Enter steps here
    Given The query parameters
     | param_name | param_value |
     | param      | value       |
