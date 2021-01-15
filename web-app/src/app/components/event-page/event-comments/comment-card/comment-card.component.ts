import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { AppComment } from 'src/app/models/comment.interface';

@Component({
  selector: 'app-comment-card',
  templateUrl: './comment-card.component.html',
  styleUrls: ['./comment-card.component.scss']
})
export class CommentCardComponent implements OnInit {
  @Input()
  comment: AppComment;
  @Input()
  username: string;
  @Output()
  deleteString: EventEmitter<string> = new EventEmitter<string>();

  constructor() { }

  ngOnInit(): void {
  }

  deleteComment(): void{
    console.log(this.comment.id);
    this.deleteString.emit(this.comment.id);
  }
}
