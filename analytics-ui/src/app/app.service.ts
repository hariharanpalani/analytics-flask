import { Observable } from "rxjs/Observable";
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable()
export class AppService {
    constructor(private http: HttpClient) {

    }

    getData(page:number): Observable<any> {
        return this.http.get(`http://localhost:5000/getdata?page=${page}`);
    }
}