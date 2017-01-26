Feature: Test 11Paths APIs
  # Enter feature description here

  Scenario: Try to clean a File with Latch using an invalid secret
    # Enter steps here
    Given The API endpoint "https://latch.elevenpaths.com"
      # And The API proxy "http://localhost:8080"
      And The API resource "/ExternalApi/CleanFile"
      And 11Paths-Authorization with application id "nBDbNL8Ae7uzyZhvgNyg" and secret "1Nz4fpbTNJcvPPQL7vYwgtZChMgdnNyGH8DB2nia"
      And The body files
       | param_name   | path_to_file              |
       | file         | tests/resources/file.pdf  |
      And The default renderer
    When I send a HTTP "POST" request
    Then The HTTP status code should be "404"


  Scenario: Try to clean a File with Latch using an invalid secret
    # Enter steps here
    Given The API endpoint "https://mockapi.sdklib.org"
      # And The API proxy "http://localhost:8080"
      And The API resource "/some/path/"
      And The headers
       | header_name   | header_value   |
       | x-header      | Hello          |
      And Authorization-Basic with username "user" and password "Passw0rd"
      And The query parameters
       | param_name   | param_value   |
       | param        | value         |
    When I send a HTTP "GET" request
    Then The HTTP status code should be "404"


  Scenario: Try to pair a Latch application using an invalid secret
    # Enter steps here
    Given The API endpoint "https://latch.elevenpaths.com"
      # And The API proxy "http://localhost:8080"
      And The parameterized API resource "/api/%(version)s/pair/%(pairing_code)s" with these parameter values
       | key           | value   |
       | version       | 1.0     |
       | pairing_code  | 123456  |
      And 11Paths-Authorization with application id "nBDbNL8Ae7uzyZhvgNyg" and secret "1Nz4fpbTNJcvPPQL7vYwgtZChMgdnNyGH8DB2nia"
    When I send a HTTP "GET" request
    Then The HTTP status code should be "200"
     And The response body should be this JSON
       """
       {"error":{"code":102,"message":"Invalid application signature"}}
       """
