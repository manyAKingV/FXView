import requests from "@/utlis/requests";
export function info(){
    return requests({
        url:"/api/",
        method:"GET"
    })
}