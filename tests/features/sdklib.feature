Feature: Sdklib sample
  # Enter feature description here

  Scenario: Github repositories search API
    # Enter steps here
    Given The API endpoint "https://api.github.com"
      #And The API proxy "http://localhost:8080"
      And The API resource "/orgs/%(organization)s/repos" with these parameter values
       | key           | value   |
       | organization  | octokit |
      And The headers
       | header_name | header_value                     |
       | Accept      | application/vnd.github.v3+json   |
       |User-Agent   | Hello-Agent!                     |
    When I send a HTTP "GET" request
    Then The HTTP status code should be "200"


  Scenario: scenario 2
    # Enter steps here
    Given The headers
     | header_name | header_value |
     | x-header    | something    |


  Scenario: scenario 3
    # Enter steps here
    Given The query parameters
     | param_name | param_value |
     | param      | value       |


  Scenario: scenario 4
    # Enter steps here
    Given The body files
     | param_name | path_to_file       |
     | param      | /path/to/file.txt  |