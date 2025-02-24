hello-user = Hello <b>{ $username }</b>!

             Issue the command /del to see the pending message deletion

will-delete = This message will be deleted after { $delay ->
                [one] { $delay } second
               *[other] { $delay } seconds
              }

no-copy = This type of update is not supported by the send_copy method