import c4d

def main():
    doc.StartUndo()  # アンドゥの開始

    materials = doc.GetMaterials()
    material_dict = {}

    # 同じ名前のマテリアルを辞書に分類
    for mat in materials:
        mat_name = mat.GetName()

        if mat_name not in material_dict:
            material_dict[mat_name] = [mat]
        else:
            material_dict[mat_name].append(mat)

    # 同名のマテリアルを統合
    for mat_name, mat_list in material_dict.items():
        main_material = mat_list[0]

        for mat in mat_list[1:]:
            replace_material(main_material, mat)
            doc.AddUndo(c4d.UNDOTYPE_DELETE, mat)  # アンドゥ操作を追加
            mat.Remove()

    doc.EndUndo()  # アンドゥの終了
    c4d.EventAdd()  # ビューポートの更新

def replace_material(new_material, old_material):
    for obj in doc.GetObjects():
        tags = obj.GetTags()
        for tag in tags:
            if tag.GetType() == c4d.Ttexture:
                if tag[c4d.TEXTURETAG_MATERIAL] == old_material:
                    tag[c4d.TEXTURETAG_MATERIAL] = new_material
                    doc.AddUndo(c4d.UNDOTYPE_CHANGE, tag)  # アンドゥ操作を追加

if __name__ == '__main__':
    main()
