import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';
import { AppComment } from 'src/app/models/comment.interface';
import { AuthService } from 'src/app/services/auth.service';
import { User } from 'src/app/models/user';
@Component({
  selector: 'app-event-comments',
  templateUrl: './event-comments.component.html',
  styleUrls: ['./event-comments.component.scss']
})
export class EventCommentsComponent implements OnInit {
  @Input() comment = '';
  @Input() eventId: string;
  public comments: AppComment[];
  public user: User;

  constructor(private apiService: ApiService, public authService: AuthService) {}

  ngOnInit(): void {
    this.getComments();
    this.authService.currentUser$.subscribe((user) => this.user = user);
  }

  public deleteComment(commentId: string): void {
    console.log(commentId);
    this.apiService.deleteComment(this.eventId, commentId).subscribe(() => this.getComments());
  }


  private getComments(): void{
    this.apiService.getComments(this.eventId).subscribe((components) => {
      console.log(components);
      this.comments = Object.values(components.items);
    });
  }


  sendComment(): void{
      if (this.comment.length > 0) {
        this.apiService.addComment(this.comment, this.eventId).subscribe((comment) => {
          this.comments = [...this.comments, comment];
        });
        this.comment = '';
      }
  }
}
