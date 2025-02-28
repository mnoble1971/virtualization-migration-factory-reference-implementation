oc apply -k projects/nginx

crictl ps
get into a pod:  crictl exec -it b3eb9e1462f52 -- /bin/sh