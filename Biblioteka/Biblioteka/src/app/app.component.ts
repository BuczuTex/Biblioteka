import { Component } from '@angular/core';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [ApiService]
})
export class AppComponent {
  books = [{autor: "test"}];

  constructor(private api: ApiService){
    this.getBooks();
  }
  getBooks = () => {
    this.api.getAllBooks().subscribe(
      data => {
        this.books = data;
      },
      error => {
        console.log(error);
      }
    )
  }
}
