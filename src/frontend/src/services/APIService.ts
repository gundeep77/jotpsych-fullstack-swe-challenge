class APIService {
  private static instance: APIService;
  private baseUrl: string;
  private appVersion: string;

  private constructor() {
    this.baseUrl = "http://localhost:3002";
    this.appVersion = "1.0.0";
  }

  public static getInstance(): APIService {
    if (!APIService.instance) {
      APIService.instance = new APIService();
    }
    return APIService.instance;
  }

  public async request(
    endpoint: string,
    method: string,
    body?: any,
    auth: boolean = false
  ): Promise<any> {
    const headers: HeadersInit = {
      "Content-Type": "application/json",
      "app-version": this.appVersion,
    };

    if (auth) {
      // get access token somehow
      const token = document.cookie.split("; ").find(row=> row.startsWith("token="))?.split("=")[1];
      if(token){
        headers["Authorization"] = `Bearer ${token}`;
      }
    
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(response.statusText);
    }

    return response.json();
  }
}

export default APIService.getInstance();
