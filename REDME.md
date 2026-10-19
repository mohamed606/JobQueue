1- The Worker will be responsible for the status because it knows the retry policy so after a job failed it know whether
to retry or mark it as failed and this leave Job very simple all it cares about is executing the function

2- max_attempts in the retry policy is the total number of attempts accepted by a policy before failing