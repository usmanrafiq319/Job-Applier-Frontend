import { Component, computed, input } from '@angular/core';

export type BadgeTone =
  | 'neutral'
  | 'info'
  | 'success'
  | 'warning'
  | 'danger';

@Component({
  selector: 'app-status-badge',
  imports: [],
  templateUrl: './status-badge.html',
  styleUrl: './status-badge.css',
})
export class StatusBadge {

  readonly label =
    input.required<string>();

  readonly tone =
    input<BadgeTone>('neutral');


  protected readonly cssClass =
    computed(() => {

      switch (this.tone()) {

        case 'success':
          return 'badge badge-success';

        case 'warning':
          return 'badge badge-warning';

        case 'danger':
          return 'badge badge-danger';

        case 'info':
          return 'badge badge-info';

        default:
          return 'badge badge-neutral';

      }

    });

}
