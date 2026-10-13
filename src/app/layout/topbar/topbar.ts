import { Component ,  output} from '@angular/core';


@Component({

  selector: 'app-topbar',

  imports: [],

  templateUrl: './topbar.html',

  styleUrl: './topbar.css'

})
export class Topbar {

  readonly menuRequested =
    output<void>();


  protected openMenu(): void {

    this.menuRequested.emit();

  }

}
