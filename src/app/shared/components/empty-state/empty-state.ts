import {
  Component,
  input,
  output
} from '@angular/core';

@Component({
  selector: 'app-empty-state',
  imports: [],
  templateUrl: './empty-state.html',
  styleUrl: './empty-state.css'
})
export class EmptyState {

  readonly icon =  input('⌕');

  readonly title =
    input.required<string>();

  readonly description =
    input<string | null>(null);

  readonly actionLabel =
    input<string | null>(null);


  readonly actionRequested =
    output<void>();

}