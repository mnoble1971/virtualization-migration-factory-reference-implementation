helm install test-mike .
oc get deployments
oc get svc
oc expose svc/test-app
oc get routes
oc get pods -o wide