export function getBaseUrl() {
    const getUrl = window.location;
    const BASEURL = getUrl.protocol + "//" + getUrl.host + "/";
    return BASEURL;
}
export default {};