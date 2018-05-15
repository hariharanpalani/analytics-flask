import { Component, OnInit } from '@angular/core';
import { columns } from './columns';
import { AppService } from './app.service';
import 'rxjs/add/operator/map';
import { LazyLoadEvent } from 'primeng/components/common/lazyloadevent';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';
  columns = columns;
  data:any[];
  totalRecords = 4000;

  constructor(private service: AppService) {
  }

  loadCarsLazy(event: LazyLoadEvent) {
    console.log(event);
    let page =(event.first / event.rows) + 1;
    this.service.getData(page).subscribe(result => this.data = result);
  }
}
