from DAL.progress_repository import ProgressDAL

class ProgressLogic:
    def __init__(self):
        self.progress_dal = ProgressDAL()

    def update_progress(self, progress_type, username, kanji, is_correct):
        progress = self.progress_dal.get_kanji_progress(progress_type, username, kanji)

        # Si no hay progreso previo, inicializamos uno nuevo
        if not progress:
            errores = 1 if not is_correct else 0
            correctas = 1 if is_correct else 0
        else:
            errores = progress.errores + (0 if is_correct else 1)
            correctas = progress.correctas + (1 if is_correct else 0)

        self.progress_dal.save_progress(progress_type, username, kanji, errores, correctas)


    def get_user_progress_summary(self, progress_type, username):
        progress_list = self.progress_dal.get_user_progress(progress_type, username)

        total_errores = sum(p.errores for p in progress_list)
        total_correctas = sum(p.correctas for p in progress_list)

        return {
            "total_errores": total_errores,
            "total_correctas": total_correctas,
            "kanji_estudiados": len(progress_list)
        }


    def list_kanji_for_revision(self, progress_type, username):
        progress_list = self.progress_dal.get_user_progress(progress_type, username)
        kanji_to_review = [p.kanji for p in progress_list if p.errores > 2 or p.correctas < 3]
        return kanji_to_review


    def get_user_progress_history(self, progress_type, username):
        progress_list = self.progress_dal.get_user_progress(progress_type, username)

        history = [
            {
                "kanji": p.kanji,
                "errores": p.errores,
                "correctas": p.correctas,
            }
            for p in progress_list
        ]

        return history