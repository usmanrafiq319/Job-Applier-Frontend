import { Component, computed, input } from '@angular/core';

@Component({
  selector: 'app-match-score',
  imports: [],
  templateUrl: './match-score.html',
  styleUrl: './match-score.css',
})
export class MatchScore {

  readonly score =  input.required<number>();

  readonly showLabel =  input(true);


  protected readonly cssClass =
    computed(() => {

      const score =
        this.score();

      if (score >= 80) {
        return 'badge badge-success';
      }

      if (score >= 60) {
        return 'badge badge-warning';
      }

      return 'badge badge-danger';

    });


  protected readonly label =
    computed(() => {

      const score =
        this.score();

      if (score >= 80) {
        return 'Strong';
      }

      if (score >= 60) {
        return 'Possible';
      }

      return 'Low';

    });

}
